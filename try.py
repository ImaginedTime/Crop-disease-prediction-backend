ground_nut_class_names = ['GROUNDNUT LEAF SPOT (EARLY AND LATE)', 'GROUNDNUT ROSETTE', 'GROUNDNUT RUST', 'GROUNDNUT ALTERNARIA LEAF SPOT', 'GROUNDNUT HEALTHY']
wheat_class_names = ['WHEAT BROWN RUST', 'WHEAT HEALTHY', 'WHEAT YELLOW RUST']
rice_class_names = ['RICE BACTERIAL BLIGHT', 'RICE BLAST', 'RICE HEALTHY', 'RICE NECK BLAST']
corn_class_names = ['CORN COMMON RUST', 'CORN GREY LEAF SPOT', 'CORN HEALTHY', 'CORN NORTHERN LEAF BLIGHT']
potato_class_names = ['POTATO EARLY BLIGHT', 'POTATO HEALTHY', 'POTATO LATE BLIGHT']
sugarcane_class_names = ['SUGARCANE BACTERIAL BLIGHT', 'SUGARCANE HEALTHY', 'SUGARCANE RED ROT', 'SUGARCANE YELLOW RUST']
tea_class_names = ['TEA ALGAL LEAF', 'TEA ANTRACNOSE', 'TEA HEALTHY', 'TEA LEAF BLIGHT', 'TEA RED LEAF SPOT', 'TEA RED SCAB']
soyabean_class_names = ['SOYABEAN BACTERIAL LEAF BLIGHT', 'SOYABEAN DRY LEAF', 'SOYABEAN HEALTHY', 'SOYABEAN SEPTORIA BROWN SPOT', 'SOYABEAN VEIN NECROSIS']
cotton_class_names = ['Aphids', 'Army worm', 'Bacterial Blight', 'Healthy', 'Powdery Mildew', 'Target spot']
tomato_class_names = ['TOMATO BACTERIAL SPOT', 'TOMATO EARLY BLIGHT', 'TOMATO HEALTHY', 'TOMATO LATE BLIGHT', 'TOMATO LEAF MOLD', 'TOMATO MOSAIC VIRUS', 'TOMATO SEPTORIA LEAF SPOT', 'TOMATO TARGET SPOTS', 'TOMATO YELLOW LEAF CURL VIRUS']


# for each disease name, do ' '.join(name.split())
ground_nut_class_names = [' '.join(name.split()) for name in ground_nut_class_names]
wheat_class_names = [' '.join(name.split()) for name in wheat_class_names]
rice_class_names = [' '.join(name.split()) for name in rice_class_names]
corn_class_names = [' '.join(name.split()) for name in corn_class_names]
potato_class_names = [' '.join(name.split()) for name in potato_class_names]
sugarcane_class_names = [' '.join(name.split()) for name in sugarcane_class_names]
tea_class_names = [' '.join(name.split()) for name in tea_class_names]
soyabean_class_names = [' '.join(name.split()) for name in soyabean_class_names]
cotton_class_names = [' '.join(name.split()) for name in cotton_class_names]
tomato_class_names = [' '.join(name.split()) for name in tomato_class_names]

print(ground_nut_class_names)
print(wheat_class_names)
print(rice_class_names)
print(corn_class_names)
print(potato_class_names)
print(sugarcane_class_names)
print(tea_class_names)
print(soyabean_class_names)
print(cotton_class_names)
print(tomato_class_names)

