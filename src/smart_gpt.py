import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Grossmend/rudialogpt3_medium_based_on_gpt2")
model = AutoModelForCausalLM.from_pretrained(
    "Grossmend/rudialogpt3_medium_based_on_gpt2"
)

device = "cuda"
model.to(device)


def get_length_param(text: str) -> str:
    tokens_count = len(tokenizer.encode(text))
    if tokens_count <= 15:
        len_param = "1"
    elif tokens_count <= 50:
        len_param = "2"
    elif tokens_count <= 256:
        len_param = "3"
    else:
        len_param = "-"
    return len_param


def answer_gasya_gpt(input_user: str, chat_history_ids=None):

    new_user_input_ids = tokenizer.encode(
        f"|0|{get_length_param(input_user)}|"
        + input_user
        + tokenizer.eos_token
        + "|1|1|",
        return_tensors="pt",
    ).to(device)

    bot_input_ids = (
        torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
        if chat_history_ids is not None
        else new_user_input_ids
    )

    chat_history_ids = model.generate(
        bot_input_ids,
        num_return_sequences=1,
        max_length=512,
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=50,
        top_p=0.9,
        temperature=0.6,
        mask_token_id=tokenizer.mask_token_id,
        eos_token_id=tokenizer.eos_token_id,
        unk_token_id=tokenizer.unk_token_id,
        pad_token_id=tokenizer.pad_token_id,
        device=device,
    )
    answer = {
        tokenizer.decode(
            chat_history_ids[:, bot_input_ids.shape[-1] :][0], skip_special_tokens=True
        )
    }

    chat_history_ids = chat_history_ids[:, :512]

    return answer, chat_history_ids
