from ML_Pipeline.db import ContextManager, IntentFlow
from ML_Pipeline.infer import interpreter


def process_message(message, client_id, chat_id):
    """
    :param message: chat message from the user ,to be processed by the ML models
    :param client_id: client id
    :param chat_id: chat id for storing context
    :return: returns response / prompt for the un - fulfilled slots defined for the given intent
    """
    """ take chat message,predicts from rasa nlu pipeline"""
    response = interpreter.parse(message)
    intent_pred = response['intent']['name']
    intent_conf = response['intent']['confidence']

    """Check if the conf is > 90% or else intent is None"""
    intent = None
    if intent_conf > 0.90:
        intent = intent_pred

    entities_pred = response['entities']

    """ Init the context object by client and chat id"""

    context_manager = ContextManager(client_id, chat_id)
    '''Check if there is an existing intent'''
    '''if yes, check predicted now is same or not, if same fine, if not, promt user , if they wants to change??'''  ## TODO
    try:
        context = context_manager.get_context()
        if "intent" in context.keys():
            intent_context = context['intent']
            """check if the intent predicted and intent stored in the context are same or not!!"""
            if intent_context == intent:
                intent = intent_context
            else:
                if intent:
                    return "Do you want to change the intent?"
                else:
                    """it means there is no intent now, so we will continue the intent in context"""
                    intent = intent_context
    except:
        """No context has been saved yet for this chat yet!! """
        if intent:
            context_manager.update_slots(intent=intent)

    if entities_pred:
        for each_ent in entities_pred:
            """
            Push each entity label and text if the thers>0.6 as the context
            """
            entity = each_ent['entity']
            value = each_ent['value']
            conf = each_ent['confidence']
            if conf > 0.60:
                context_manager.update_slots(entity=entity)
    """Get the slots for that intent ,given chat_id"""
    response = context_manager.get_slots(intent)
    if response:
        prompt_question = response[0]['prompt']
        return prompt_question
    else:
        """get the api response , given client id, runs and returns response"""
        intent_obj = IntentFlow(client_id)
        response = intent_obj.extract_api(intent)
        return response
