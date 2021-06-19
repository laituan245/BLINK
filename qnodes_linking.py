import argparse
import blink.main_dense as main_dense
from utils import visualize_el_preds

models_path = "models/" # the path where you stored the BLINK models

config = {
    "test_entities": None,
    "test_mentions": None,
    "interactive": False,
    "top_k": 10,
    "biencoder_model": models_path+"biencoder_wiki_large.bin",
    "biencoder_config": models_path+"biencoder_wiki_large.json",
    "entity_catalogue": models_path+"entity.jsonl",
    "entity_encoding": models_path+"all_entities_large.t7",
    "crossencoder_model": models_path+"crossencoder_wiki_large.bin",
    "crossencoder_config": models_path+"crossencoder_wiki_large.json",
    "fast": False, # set this to be true if speed is a concern
    "output_path": "logs/" # logging directory
}

args = argparse.Namespace(**config)

models = main_dense.load_models(args, logger=None)

raw_data = [
    # Spread Virus
    ['Spread Virus', 'what is the best way to keep from', 'spreading', 'the virus through coughing or sneezing?'],
    ['Spread Virus', 'Farmers quickly mobilized to fight the misperceptions that pigs could', 'spread', 'the disease'],
    ['Spread Virus', 'In the UK, Asians have been punched in the face, accused of', 'spreading', 'coronavirus'],
    # Wear Mask
    ['Wear Mask', 'Pence chose not to', 'wear', "a face mask during the tour despite the facility's policy"],
    ['Wear Mask', 'It should not be necessary for workers to', 'wear', 'facemasks routinely when in contact with the public.'],
    ['Wear Mask', 'The WHO offers a conditional recommendation that health care providers also', 'wear', 'a separate head cover that protects the head and neck.'],
    # Prevent Spread
    ['Prevent Spread', 'Infection prevention and control measures are critical to', 'prevent', 'the possible spread of MERS-CoV in health care facilities'],
    ['Prevent Spread', 'A vaccine can', 'mitigate', 'spread, but not fully prevent the virus circulating.'],
    ['Prevent Spread', 'Asymptomatic infection could also potentially be directly harnessed to', 'mitigate', 'transmission.'],
    # Delay Gathering
    ['Delay Gathering', "The 2020 edition of the Cannes Film Festival, was left in limbo following an announcement from the festival's organizers that the gathering could be", "delayed", "until the June or early June"],
    ['Delay Gathering', 'States with EVD should consider', 'postponing', 'mass gatherings until EVD transmission is interrupted.'],
    ['Delay Gathering', 'On Thursday, leaders of the Church of Jesus Christ of Latter - day Saints told its 15 million members worldwide all public gatherings would be', 'suspended', 'until further notice.'],
    # Vaccinate People
    ['Vaccinate People', 'All persons in a recommended vaccination target group should be', 'vaccinated', 'with the 2009 H1N1 monovalent vaccine and the seasonal Influenza vaccine.'],
    ['Vaccinate People', 'U.K. will start', 'immunizing', 'people against COVID-19 on Tuesday, Officials Say.'],
    ['Vaccinate People', '"In the Samoan language there is no word for bacteria or virus" says Henrietta Aviga, a nurse travelling around villages to', 'vaccinate', 'and educate families.'],
    # Infect Disease
    ['Infect Disease', 'In pregnant women who become', 'infected', 'the virus can affect the foetus resulting in birth defects.'],
    ['Infect Disease', 'The protective equipment helps prevent health - care workers from becoming', 'infected', 'and spreading the disease , but it is running in short supply at a number of US hospitals.'],
    ['Infect Disease', 'Influenza D viruses primarily affect cattle and are not known to', 'infect', 'or cause illess in people.'],
    # Control Outbreak
    ['Control Outbreak', 'AusMAT is one of several teams that have travelled from overseas to help Samoa ', 'manage', 'this outbreak.'],
    ['Control Outbreak', 'Authorities are struggling to prepare Haiti for the coming storm , as well as', 'contain', 'the outbreak [Reuters].'],
    ['Control Outbreak', 'These deaths are believed to be the first resulting from resistance to international efforts to', 'curb', 'the Ebola outbreak in the region , Reuters reported.'],
    # Develop Symptom
    ['Develop Symptom', "But he said there was a good chance that the women 's babies will not possibly", 'develop', 'abnormalities related to the Zika virus.'],
    ['Develop Symptom', 'Many infants and children', 'develop', 'high fevers with minor viral illnesses.'],
    ['Develop Symptom', 'The woman spent five days in the hospital after', 'developing', 'diarrhea and dehydration , classic symptoms of cholera , following her return from Haiti , where she had spent time in the Artibonite region.'],
]

# Build data_to_link
data_to_link = []
for ix, (inst_type, ctx_left, mention, ctx_right) in enumerate(raw_data):
    data = {
        "id": ix,
        "label": "unknown",
        "label_id": -1,
        "context_left": ctx_left.lower(),
        "mention": mention.lower(),
        "context_right": ctx_right.lower(),
    }
    data_to_link.append(data)
_, _, _, _, _, predictions, scores, = main_dense.run(args, None, *models, test_data=data_to_link)

# Build data_with_predictions
data_and_predictions = []
for data, prediction in zip(raw_data, predictions):
    data_and_predictions.append({
        'type': data[0], 'context_left': data[1], 'mention': data[2], 'context_right': data[3],
        'top_entities': [
            {'id': p[0], 'title': p[1], 'text': p[2], 'url': p[3]} for p in prediction[:5]
        ]
    })

# visualization
visualize_el_preds(data_and_predictions)
