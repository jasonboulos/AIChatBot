// Define a Conversation Interface
export interface Conversation {
    question: string;
    answer: string;
  }
  
  // Define a Chat Interface
  export interface Chat {
    title: string;                    
    conversations: Conversation[];    
    date: Date;                       
  }
  