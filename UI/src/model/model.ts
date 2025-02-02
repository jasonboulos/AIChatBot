export interface Conversation {
    question: string;
    answer: string;
    sources: string[];
  }
  
  export interface Chat {
    title: string;                    
    conversations: Conversation[];   
    showSources?: boolean; 
    date: Date;                       
  }
  