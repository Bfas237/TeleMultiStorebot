

from pyrogram import Client, Filters
exec_running_text = "<b>Exec Code:</b>\n<code>{code}</code>\n<b>Running...</b>"
exec_success_text = "<b>Exec Code:</b>\n<code>{code}</code>\n<b>Success</b>"
exec_error_text = "<b>Exec Code:</b>\n<code>{code}</code>\n<b>Error:</b>\n<code>{error}</code>"
exec_result_text = "<b>Exec Code:</b>\n<code>{code}</code>\n<b>Result:</b>\n<code>{result}</code>" 
prefix="!"
@Client.on_message(Filters.user(197005208) & Filters.command("exec", prefix))
def execute(c, m):
    colength = len("exec") + len(prefix) 
    code = m.text[colength:].lstrip() 
    mm = m.reply(exec_running_text.replace('{code}', code), parse_mode="HTML")
    try:
        exec('def __ex(c, m): ' + ''.join('\n ' + l for l in code.split('\n')))
        result = locals()['__ex'](c, m)
    except Exception as e: 
        c.edit_message_text(m.chat.id, mm.message_id, exec_error_text.replace('{code}', code).replace('{error}', str(e)), parse_mode="HTML")

    else:
        if result:
            c.edit_message_text(m.chat.id, mm.message_id, exec_result_text.replace('{code}', code).replace('{result}', str(result)), parse_mode="HTML")

        else:   
            c.edit_message_text(m.chat.id, mm.message_id, exec_success_text.replace('{code}', code), parse_mode="HTML")
             
  