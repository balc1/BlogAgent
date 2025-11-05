from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog

class BlogNode:
    """
    A class to represent he blog node
    """

    def __init__(self,llm):
        self.llm=llm

    
    def title_creation(self,state:BlogState):
        """
        create the title for the blog
        """

        if "topic" in state and state["topic"]:
            prompt="""
                   You are an expert blog content writer. Use Markdown formatting. Generate
                   a blog title for the {topic}. This title should be creative and SEO friendly

                   """
            
            sytem_message=prompt.format(topic=state["topic"])
            print(sytem_message)
            response=self.llm.invoke(sytem_message)
            print(response)
            return {"blog":{"title":response.content}}
        
    def content_generation(self,state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}
        
    def translation(self,state:BlogState):
        """
        Translate the content to the specified language.
        """
        
        # 1. Prompt'u hem başlığı hem de içeriği çevirecek şekilde güncelleyelim
        translation_prompt="""
        You are a professional translator. Translate BOTH the 'title' and 'content' 
        of the following blog post into {current_language}.
        
        - You MUST return a complete blog post in the correct Pydantic/JSON format, 
          containing both the translated 'title' and 'content'.
        - Maintain the original tone, style, and formatting (like Markdown).

        ORIGINAL TITLE:
        {blog_title}

        ORIGINAL CONTENT:
        {blog_content}
        """
        
        print(f"Translating to {state['current_language']}...")
        
        # 2. State'den hem başlığı (title) hem de içeriği (content) alalım
        original_title = state["blog"]["title"]
        original_content = state["blog"]["content"]
        
        messages=[
            HumanMessage(
                translation_prompt.format(
                    current_language=state["current_language"], 
                    blog_title=original_title, 
                    blog_content=original_content
                )
            )
        ]

        # 3. LLM'den Blog yapısında (title ve content) çevrilmiş çıktıyı isteyelim
        # Bu satır artık hata vermeyecek çünkü LLM'in çevirmesi için 
        # gereken tüm bilgiler (title ve content) ona verildi.
        translated_blog = self.llm.with_structured_output(Blog).invoke(messages)
        
        # 4. (ÇÖZÜM) State'i doğru formatta güncelleyelim
        # translated_blog zaten {"title": "...", "content": "..."} yapısındadır.
        # Biz de bunu doğrudan blog'un yerine koyuyoruz.
        return {"blog": translated_blog}

    def route(self, state: BlogState):
        return {"current_language": state['current_language'] }
    

    def route_decision(self, state: BlogState):
        """
        Route the content to the respective translation function.
        """
        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "french": 
            return "french"
        else:
            return state['current_language']