#!/usr/bin/env python3
"""
    Scripts for converting task 3 output to task 1 output format 

"""
import argparse
import json
import os

END_OF_RESPONSE = '<EOR>'



def convertToTask1_fashion(lines, dialogue_id) :
    output = {
        "dialog_id" : dialog_id, 
        "predictions" : [

        ]
    }
    turn_id = 0 
    prediction = {
        "turn_id" : turn_id,
        "action" : 'None',
        "attributes": {
                "attributes" : []
        },
         "action_log_prob" : {
            "SearchDatabase" : 0,
            "SearchMemory" : 0,
            "SpecifyInfo" : 0,
            "AddToCart" : 0,
            "None" : 0
        }
    }
    for line in lines : 
        if not '<EOR>' in line :
            output["predictions"].append(prediction)
        else : 
            output["predictions"].append(convertTurn_fashion(line.split(END_OF_RESPONSE)[1], turn_id))
        turn_id += 1

    return output 

def convertTurn_fashion(toParse,turn_id):
    prediction = {
        "turn_id" : turn_id,
        "action" : 'None',
        "attributes": {
            "attributes" : []
        },
        "action_log_prob" : {
            "SearchDatabase" : 0,
            "SearchMemory" : 0,
            "SpecifyInfo" : 0,
            "AddToCart" : 0,
            "None" : 0
        }
    }
    if not toParse :
        return prediction
    action = toParse.split("[")[0].strip()
    if len(toParse.split("[")) < 1 : 
        return prediction 
    prediction["action"] = action 
    if len(toParse.split("[")) < 2 : 
        return prediction 
    rest = toParse.split("[")[1].strip()
    attributes = rest.split("]")[0]
    if attributes : 
        listAttr = attributes.split(",")
        for attribute in listAttr : 
            if len(attribute.split("=")) >= 1 : 
                for i in range(len(attributes.split("="))):
                    name = attribute.split("=")[i].strip()
                    prediction["attributes"]["attributes"].append(name)
            else :
                prediction["attributes"]["attributes"]= []

    return prediction


def convertToTask1_furniture(lines, dialogue_id) :
    output = {
        "dialog_id" : dialog_id, 
        "predictions" : [

        ]
    }
    prediction = {
        "action" : 'None',
        "attributes": {
        },
        "turn_id" : 0,
         "action_log_prob" : {
            "SearchFurniture" : 0,
            "FocusOnFurniture" : 0,
            "SpecifyInfo" : 0,
            "Rotate" : 0,
            "NavigateCarousel" : 0,
            "AddToCart" : 0,
            "None" : 0
        }
    }

    turn_id = 0 
    for line in lines : 
        if not '<EOR>' in line :
            output["predictions"].append(prediction)
        else : 
            output["predictions"].append(convertTurn_furniture(line.split(END_OF_RESPONSE)[1],turn_id))
        turn_id += 1 
    return output 

def convertTurn_furniture(toParse,turn_id):
    prediction = {
        "action" : 'None',
        "attributes": { 
        },
        "turn_id": turn_id,
        "action_log_prob" : {
            "SearchFurniture" : 0,
            "FocusOnFurniture" : 0,
            "SpecifyInfo" : 0,
            "Rotate" : 0,
            "NavigateCarousel" : 0,
            "AddToCart" : 0,
            "None" : 0
        }
    }
    
    if not toParse :
            return prediction
    action = toParse.split("[")[0].strip() 
    if action == "SearchFurniture" :      ## add attribute key values for each action 
        prediction["attributes"]["furnitureType"] = 'None'
        prediction["attributes"]["color"] = 'None'
    elif action == "FocusOnFurniture" : 
        prediction["attributes"]["position"] = 'None'
    elif action == "SpecifyInfo" :
        prediction["attributes"]["matches"] = 'None'
        prediction["attributes"]["attributes"] ='None'
    elif action == "Rotate" :
        prediction["attributes"]["direction"] = 'None'
    elif action == "NavigateCarousel" :
        prediction["attributes"]["navigate_direction"] = 'None'
    if len(toParse.split("[")) < 1 : 
        return prediction 
    prediction["action"] = action 
    if len(toParse.split("[")) < 2 : 
        return prediction 
    rest = toParse.split("[")[1].strip()
    attributes = rest.split("]")[0]
    if attributes : 
        listAttr = attributes.split(",")
        for attribute in listAttr : 
            name = attribute.split("=")[0].strip()
            if len(attribute.split("=")) == 2 : 
                value = attribute.split("=")[1].strip()
                prediction["attributes"][name] = value 
             
    return prediction

if __name__ == '__main__':
    # Parse input args
    parser = argparse.ArgumentParser()  
    parser.add_argument('--input_predicted_file', type=str, 
                        help='path for predicted results from task 3(.txt)') 
    parser.add_argument('--input_predict_json',  
                        help='path for predict json') 
    parser.add_argument('--output_path',
                        help='output file path for converted results (.json')
    parser.add_argument('--domain',
                        help='domain')

    args = parser.parse_args()
    input_predicted_file = args.input_predicted_file
    output_path = args.output_path
    input_predict_json = args.input_predict_json 
    domain = args.domain 
    idx=0
    dialog_ids = [] 
    turn_length = []
    result = [] 
    with open(input_predict_json, "r") as file:
        dials = json.load(file)
        for dialogue in dials['dialogue_data'] : 
            leng = len(dialogue['dialogue'])
            dialog_ids.append(dialogue['dialogue_idx'])
            turn_length.append(leng)
    

    file = open(input_predicted_file,"r") 

    i = 0  
    for dialog_id in dialog_ids : 
        lines = []
        for t in range(turn_length[i]) :
            lines.append(next(file))
        if domain == "furniture" : 
            result.append(convertToTask1_furniture(lines,dialog_id)) 
        else : 
            result.append(convertToTask1_fashion(lines,dialog_id))
        i+=1
    
      
    final_json = {}
    with open(output_path, "w") as json_file:
        json.dump(result, json_file)


