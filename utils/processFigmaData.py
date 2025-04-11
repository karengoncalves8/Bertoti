def process_figma_data(figma_data):
    elements = []

    def process_children(children):
        for child in children:
            if child['type'] == 'TEXT':
                element = {
                    "type": "text",
                    "name": child['name'],
                    "position": {
                        "x": child['absoluteBoundingBox']['x'],
                        "y": child['absoluteBoundingBox']['y']
                    },
                    "size": {
                        "width": child['absoluteBoundingBox']['width'],
                        "height": child['absoluteBoundingBox']['height']
                    },
                    "text": child.get('characters', '')
                }
                elements.append(element)

            elif child['type'] == 'RECTANGLE':
                element_type = 'input' if "Input" in child['name'] else 'button'
                
                color = None
                if 'fills' in child:
                    for fill in child['fills']:
                        if 'color' in fill:  
                            color = fill['color']
                            break  

                element = {
                    "type": element_type,
                    "name": child['name'],
                    "position": {
                        "x": child['absoluteBoundingBox']['x'],
                        "y": child['absoluteBoundingBox']['y']
                    },
                    "size": {
                        "width": child['absoluteBoundingBox']['width'],
                        "height": child['absoluteBoundingBox']['height']
                    },
                    "color": color
                }
                elements.append(element)

            elif child['type'] == 'GROUP':
                print(f"Processando grupo: {child['name']}")  
                process_children(child['children'])  

            elif child['type'] == 'VECTOR':
                image_url = None
                if 'fills' in child:
                    for fill in child['fills']:
                        if 'imageRef' in fill:
                            image_url = fill['imageRef']
                            break
                element = {
                    "type": "image",
                    "name": child['name'],
                    "position": {
                        "x": child['absoluteBoundingBox']['x'],
                        "y": child['absoluteBoundingBox']['y']
                    },
                    "size": {
                        "width": child['absoluteBoundingBox']['width'],
                        "height": child['absoluteBoundingBox']['height']
                    },
                    "image_url": image_url
                }
                elements.append(element)

    for node in figma_data['document']['children']:
        if node['type'] == 'CANVAS':  
            for child in node['children']:
                if child['type'] == 'FRAME':  
                    process_children(child['children'])  

    return {"elements": elements}
