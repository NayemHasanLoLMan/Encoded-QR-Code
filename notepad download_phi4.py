from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "microsoft/phi-4-mini"

AutoTokenizer.from_pretrained(model_id)
AutoModelForCausalLM.from_pretrained(model_id)

print("Phi-4-mini downloaded & cached.")
