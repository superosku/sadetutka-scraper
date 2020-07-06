import requests
import datetime

urls = [
    'https://www.ilmatieteenlaitos.fi/sade-ja-pilvialueet?5KbKoVoJ00CslbCZf76dWe_q=lang%253Dfi%2526map%253Dsuomi',
    'https://www.ilmatieteenlaitos.fi/sade-ja-pilvialueet?5KbKoVoJ00CslbCZf76dWe_q=lang%253Dfi%2526map%253Dsuomen-etelaosa',
    'https://www.ilmatieteenlaitos.fi/sade-ja-pilvialueet?5KbKoVoJ00CslbCZf76dWe_q=lang%253Dfi%2526map%253Dsuomen-keskiosa',
    'https://www.ilmatieteenlaitos.fi/sade-ja-pilvialueet?5KbKoVoJ00CslbCZf76dWe_q=lang%253Dfi%2526map%253Dsuomen-pohjoisosa',
]

now = datetime.datetime.now().isoformat()

for url in urls:
    name = url.split('%253D')[-1]

    response = requests.get(url)

    new_text = response.text
    current_start_index = new_text.find('anim_images_anim_anim =')

    while current_start_index >= 0:
        new_text = new_text[current_start_index:]
        current_end_index = new_text.find('")')

        array_part = new_text[:current_end_index+10]

        current_start_index = new_text.find('anim_images_anim_anim =')

        break

    image_urls = [item.strip('"') for item in array_part[34:-9].split(',')]

    time_texts = response.text[
        response.text.find('Havainnot'):
        response.text.find('</td></tr></table>')
    ]

    time_list = [
        l[l.find('"anim_image') + 18:l.find('</div></t')].replace('&nbsp;', ' ').strip()
        for l in time_texts.split('d></tr><tr><td>')
        # for l in time_texts.split('</div></td></tr>')
    ]
    time_list = [
        t.strip('>')
        for t in time_list[:-1]
        if t
    ]

    assert len(time_list) == len(time_list)

    for url, time_name in zip(image_urls, time_list):
        time_name = '_'.join(time_name.split(' '))
        output_file_name = '{}_{}_{}.png'.format(
            now,
            name,
            time_name
        )

        img_response = requests.get(url)

        with open('output/' + output_file_name, 'wb') as file_object:
            file_object.write(img_response.content)

        print('WRITTEN', output_file_name)

