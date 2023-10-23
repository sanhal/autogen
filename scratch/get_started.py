import os
import shutil
import boto3

def clear_cache():
    # Function for cleaning up cash to
    # avoid potential spill of conversation
    # between models

    # Should be run before and after each chat initialization
    folder_path = '.cache'
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)


import autogen
from autogen import AssistantAgent, UserProxyAgent

clear_cache()

bedrock = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-east-1"
)


config_list = [
    {
        "model": "anthropic.claude-v2",
        "api_type": "LiteLLM",
        "custom_llm_provider": "bedrock",
        "temperature": 1.0,
        "max_tokens_to_sample": 2000,
        "aws_bedrock_client": bedrock
    }
]





llm_config = {"config_list": config_list, "seed": 42}
user_proxy = autogen.UserProxyAgent(
   name="User_proxy",
   system_message="A human admin.",
   code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
   human_input_mode="TERMINATE"
)
coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
)
pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Creative in software product ideas.",
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(agents=[user_proxy, coder], messages=[], max_round=12)
# groupchat = autogen.GroupChat(agents=[user_proxy, coder, pm], messages=[], max_round=12)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# user_proxy.initiate_chat(manager, message="Find a latest paper about gpt-4 on arxiv and find its potential applications in software.")
user_proxy.initiate_chat(manager, message="Suggest a productive activity using https://www.boredapi.com/ api")
