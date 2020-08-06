import re
from googletrans import Translator

filepath = 'C:/Users/malep/Documents/GitHub/Hotel-Admin-Dashboard/app/translations/it/LC_MESSAGES/messages.po'
language_code = 'it'

def extract_outer_quotes(text):
    begin_idx = -1
    end_idx = -1
    
    for i, c in enumerate(text):
        if c == '"':
            if begin_idx < 0:
                begin_idx = i
            else:
                end_idx = i

    if begin_idx >= 0:
        return text[begin_idx+1:end_idx]
        
    return ''

def insert_translated_text(line, text):
    first_quote_idx = 0

    for i, c in enumerate(line):
        if c == '"':
            first_quote_idx = i
            break

    first_quote_idx += 1

    return line[ : first_quote_idx] + text + line[first_quote_idx : ]

with open(filepath, 'r') as fp:
    translator = Translator()

    cur_to_translate = ''
    start_appending = False
    new_lines = []

    for cnt, line in enumerate(fp):
        editted_line = line
        
        if line.startswith('msgstr'):
            if '%(' in cur_to_translate or cur_to_translate == '':
                print('Skipping line {} due to string substitution. Please translate manually.'.format(cnt + 1))
                cur_to_translate = ''
                start_appending = False
                new_lines.append(editted_line)
                continue

            translated_text = translator.translate(cur_to_translate, dest=language_code).text

            editted_line = insert_translated_text(line, translated_text)
                
            cur_to_translate = ''
            start_appending = False
        elif line.startswith('msgid'):
            start_appending = True
            
        if start_appending:
            cur_to_translate += extract_outer_quotes(line)

        new_lines.append(editted_line)

with open(filepath, 'wb') as fp:
    for line in new_lines:
        fp.write(line.encode("UTF-8"))

