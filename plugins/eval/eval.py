
from pyrogram import Client, Filters

RUNNING = "**Eval Expression:**\n```{}```\n**Running...**"
ERROR = "**Eval Expression:**\n```{}```\n**Error:**\n```{}```"
SUCCESS = "**Eval Expression:**\n```{}```\n**Success**"
RESULT = "**Eval Expression:**\n```{}```\n**Result:**\n```{}```"


@Client.on_message(Filters.command("eval", prefix="!"))
def eval_expression(client, message):
    expression = " ".join(message.command[1:])

    if expression:
        m = message.reply(RUNNING.format(expression))

        try:
            result = eval(expression)
        except Exception as error:
            client.edit_message_text(
                m.chat.id,
                m.message_id,
                ERROR.format(expression, error)
            )
        else:
            if result is None:
                client.edit_message_text(
                    m.chat.id,
                    m.message_id,
                    SUCCESS.format(expression)
                )
            else:
                client.edit_message_text(
                    m.chat.id,
                    m.message_id,
                    RESULT.format(expression, result)
                )