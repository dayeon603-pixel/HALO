"""Training pipelines.

Modules:
    lora_finetune   LoRA fine-tuning of KT Mi:dm 2.0 Mini on Korean scam corpus.
    evaluate        Evaluation harness computing F1, ECE, latency.
    delta_update    Weekly delta update loop that re-tunes LoRA adapter on new data.
"""
