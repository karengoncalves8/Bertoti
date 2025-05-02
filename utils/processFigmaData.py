def process_figma_data(figma_data):
    elements = []

    def process_children(children):
        for child in children:
            # Caso seja um texto
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
                    "text": child.get('characters', ''),
                    "style": {
                        "fontFamily": child.get('style', {}).get('fontFamily', ''),
                        "fontSize": child.get('style', {}).get('fontSize', 12)
                    }
                }
                elements.append(element)

            # Caso seja um retângulo ou input/button
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

            # Caso seja um grupo, chama a função recursiva para processar seus filhos
            elif child['type'] == 'GROUP' or child['type'] == 'FRAME':
                process_children(child['children'])  

            # Caso seja um vetor (imagem)
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
                    "image_url": image_url if image_url else None
                }
                elements.append(element)

    for node in figma_data['document']['children']:
        if node['type'] == 'CANVAS':  
            for child in node['children']:
                if child['type'] == 'FRAME':  
                    process_children(child['children'])  

    return {"elements": elements}
