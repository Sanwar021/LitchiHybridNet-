"""
Main experiment runner for LitchiHybridNet.
Runs training + evaluation for the proposed model and baselines across multiple seeds.
"""

import os
import sys
import json
import argparse
from pathlib import Path

import numpy as np
import torch
import yaml

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.dataset import get_dataloaders, LITCHI_CLASSES
from src.models.litchi_hybrid_net import LitchiHybridNet, CNNOnlyModel, GaborOnlyModel
from src.train.trainer import train_model
from src.eval.evaluator import evaluate_model


def load_config(config_path: str) -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def create_model(config: dict, model_type: str = "hybrid") -> torch.nn.Module:
    """Create model based on config and type."""
    mc = config["model"]
    
    if model_type == "hybrid":
        return LitchiHybridNet(
            num_classes=mc["num_classes"],
            backbone_name=mc["backbone"],
            pretrained=mc["pretrained"],
            gabor_out_features=128,
            gabor_num_scales=mc["gabor"]["num_scales"],
            gabor_num_orientations=mc["gabor"]["num_orientations"],
            gabor_kernel_size=mc["gabor"]["kernel_size"],
            gabor_learnable=mc["gabor"]["learnable"],
            gabor_min_lambda=mc["gabor"]["min_lambda"],
            gabor_max_lambda=mc["gabor"]["max_lambda"],
            fusion_type=mc["fusion"]["type"],
            fusion_reduction=mc["fusion"]["reduction"],
            hidden_dim=mc["classifier"]["hidden_dim"],
            dropout_rate=mc["classifier"]["dropout"],
        )
    elif model_type == "cnn_only":
        return CNNOnlyModel(
            num_classes=mc["num_classes"],
            backbone_name=mc["backbone"],
            pretrained=mc["pretrained"],
            hidden_dim=mc["classifier"]["hidden_dim"],
            dropout_rate=mc["classifier"]["dropout"],
        )
    elif model_type == "gabor_only":
        return GaborOnlyModel(
            num_classes=mc["num_classes"],
            gabor_out_features=256,
            gabor_num_scales=mc["gabor"]["num_scales"],
            gabor_num_orientations=mc["gabor"]["num_orientations"],
            gabor_kernel_size=mc["gabor"]["kernel_size"],
            gabor_learnable=mc["gabor"]["learnable"],
            hidden_dim=mc["classifier"]["hidden_dim"],
            dropout_rate=mc["classifier"]["dropout"],
        )
    elif model_type.startswith("baseline_"):
        # timm baseline with a different backbone
        backbone = model_type.replace("baseline_", "")
        return CNNOnlyModel(
            num_classes=mc["num_classes"],
            backbone_name=backbone,
            pretrained=True,
            hidden_dim=mc["classifier"]["hidden_dim"],
            dropout_rate=mc["classifier"]["dropout"],
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")


def run_single_experiment(
    config: dict,
    model_type: str,
    seed: int,
    device: torch.device,
) -> dict:
    """Run a single experiment (one model, one seed)."""
    
    tc = config["training"]
    experiment_name = f"{model_type}_seed{seed}"
    
    results_dir = os.path.join(PROJECT_ROOT, config["paths"]["results"], experiment_name)
    checkpoint_dir = os.path.join(PROJECT_ROOT, config["paths"]["checkpoints"])
    
    print(f"\n{'#'*70}")
    print(f" Experiment: {experiment_name}")
    print(f"{'#'*70}")
    
    # Data
    splits_dir = os.path.join(PROJECT_ROOT, config["data"]["splits_dir"])
    train_loader, val_loader, test_loader, class_names, split_counts = get_dataloaders(
        splits_dir=splits_dir,
        batch_size=config["data"]["batch_size"],
        img_size=config["data"]["img_size"],
        num_workers=config["data"]["num_workers"],
        use_class_weights=tc.get("use_class_weights", True),
    )
    
    print(f"  Data: {split_counts}")
    
    # Model
    model = create_model(config, model_type)
    total_params = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"  Model: {model_type} | Params: {total_params:,} (trainable: {trainable:,})")
    
    # Train
    train_results = train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        epochs=tc["epochs"],
        lr=tc["optimizer"]["lr"],
        weight_decay=tc["optimizer"]["weight_decay"],
        warmup_epochs=tc["scheduler"]["warmup_epochs"],
        min_lr=tc["scheduler"]["min_lr"],
        label_smoothing=config["model"]["classifier"]["label_smoothing"],
        grad_clip=tc.get("gradient_clip", 1.0),
        patience=tc["early_stopping"]["patience"],
        checkpoint_dir=checkpoint_dir,
        results_dir=results_dir,
        experiment_name=experiment_name,
        device=device,
        seed=seed,
    )
    
    # Load best checkpoint and evaluate
    checkpoint = torch.load(train_results["checkpoint_path"], map_location=device, weights_only=False)
    model.load_state_dict(checkpoint["model_state_dict"])
    
    test_metrics = evaluate_model(
        model=model,
        test_loader=test_loader,
        class_names=class_names,
        device=device,
        save_dir=results_dir,
        dataset_name=f"BDLitchi ({experiment_name})",
    )
    
    # Combine results
    result = {
        "experiment_name": experiment_name,
        "model_type": model_type,
        "seed": seed,
        "total_params": total_params,
        "trainable_params": trainable,
        "train_results": {
            "best_epoch": train_results["best_epoch"],
            "best_val_f1": train_results["best_val_f1"],
            "total_time_s": train_results["total_time_s"],
        },
        "test_metrics": {k: v for k, v in test_metrics.items() 
                        if k not in ["classification_report", "confusion_matrix"]},
    }
    
    # Save combined result
    with open(os.path.join(results_dir, "experiment_result.json"), "w") as f:
        json.dump(result, f, indent=4)
    
    return result


def aggregate_seed_results(all_results: list, model_type: str) -> dict:
    """Aggregate results across seeds: compute mean ± std."""
    metrics_keys = ["accuracy", "balanced_accuracy", "macro_f1", "weighted_f1",
                     "macro_precision", "macro_recall", "mcc", "cohen_kappa"]
    
    agg = {"model_type": model_type, "num_seeds": len(all_results)}
    
    for key in metrics_keys:
        values = [r["test_metrics"].get(key, 0) for r in all_results if r is not None]
        if values:
            agg[f"{key}_mean"] = float(np.mean(values))
            agg[f"{key}_std"] = float(np.std(values))
    
    times = [r["train_results"]["total_time_s"] for r in all_results if r is not None]
    if times:
        agg["avg_training_time_s"] = float(np.mean(times))
    
    return agg


def main():
    parser = argparse.ArgumentParser(description="Run LitchiHybridNet Experiments")
    parser.add_argument("--config", type=str, default=str(PROJECT_ROOT / "configs" / "default.yaml"))
    parser.add_argument("--model", type=str, default="hybrid",
                        help="Model type: hybrid, cnn_only, gabor_only, baseline_<backbone>")
    parser.add_argument("--seeds", type=int, nargs="+", default=None,
                        help="Seeds to run (overrides config)")
    parser.add_argument("--epochs", type=int, default=None, help="Override epochs")
    args = parser.parse_args()
    
    config = load_config(args.config)
    
    if args.seeds:
        seeds = args.seeds
    else:
        seeds = config["evaluation"]["seeds"]
    
    if args.epochs:
        config["training"]["epochs"] = args.epochs
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    print(f"Model: {args.model}")
    print(f"Seeds: {seeds}")
    
    all_results = []
    for seed in seeds:
        try:
            result = run_single_experiment(config, args.model, seed, device)
            all_results.append(result)
        except Exception as e:
            print(f"ERROR in seed {seed}: {e}")
            import traceback
            traceback.print_exc()
            all_results.append(None)
    
    # Aggregate
    valid_results = [r for r in all_results if r is not None]
    if valid_results:
        agg = aggregate_seed_results(valid_results, args.model)
        agg_path = os.path.join(PROJECT_ROOT, config["paths"]["results"], f"{args.model}_aggregated.json")
        os.makedirs(os.path.dirname(agg_path), exist_ok=True)
        with open(agg_path, "w") as f:
            json.dump(agg, f, indent=4)
        
        print(f"\n{'='*70}")
        print(f" AGGREGATED RESULTS: {args.model} ({len(valid_results)} seeds)")
        print(f"{'='*70}")
        for key in ["accuracy", "macro_f1", "mcc", "cohen_kappa"]:
            m = agg.get(f"{key}_mean", 0)
            s = agg.get(f"{key}_std", 0)
            print(f"  {key}: {m*100:.2f} +/- {s*100:.2f}%")
        print(f"{'='*70}")


if __name__ == "__main__":
    main()
