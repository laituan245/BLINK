def visualize_el_preds(data_and_predictions, output_fp='visualization.html'):
    f = open(output_fp, 'w+')

    for data in data_and_predictions:
        inst_type = data['type']
        ctx_left = data['context_left']
        mention = data['mention']
        ctx_right = data['context_right']
        # Input
        f.write(f'<span style="color:red">[{inst_type}]</span> {ctx_left} <b>{mention}</b> {ctx_right}</br></br>\n')
        # Predictions
        for p in data['top_entities']:
            eid, e_title, e_url, e_text = p['id'], p['title'], p['url'], p['text']
            f.write(f'[<a href="{e_url}">{eid}</a> <i>{e_title}</i>] ')
            f.write(f'{e_text[:200]} ...')
            f.write('</br></br>\n')
        # Separators
        f.write('</br><hr>\n')

    f.close()
    print(f'Generated a visualization file {output_fp}')
