import { Component, OnInit } from '@angular/core';
import {ChatServiceService} from '../chat-service.service'
import { Chat } from 'src/model/model';
@Component({
  selector: 'app-conversation',
  templateUrl: './conversation.component.html',
  styleUrls: ['./conversation.component.css'],
})
export class ConversationComponent implements OnInit {
  selectedChat: any;
  constructor(private chatService: ChatServiceService) {}
  ngOnInit() {
    // Subscribe to the selected chat observable
    this.chatService.selectedChat$.subscribe((chat) => {
      this.selectedChat = chat;
    });
    if(!this.selectedChat){
      this.selectedChat = {
        title:"Chat With Assistant",
        conversations: [],
        date: new Date()
      }
    }
    
  }
  userQuestion: string = ''; // User input for question
  chat: Chat = {
    title: 'Chat with Assistant',
    conversations: [],
    date: new Date(),
  };
  askQuestion() {
    if (!this.userQuestion.trim()) {
      return; // Avoid empty questions
    }
    
    const userQuestion = this.userQuestion; // Store the user's question
  
    // Initialize the chat object if it doesn't exist
    if(!this.selectedChat){
      this.selectedChat = {
        title:"Chat With Assistant",
        conversations: [],
        date: new Date()
      }
    }
  
    // Push a new conversation into the chat's conversations list
    const newConversation = { question:userQuestion, answer: 'Typing...' };
    this.selectedChat.conversations.push(newConversation);
  
  
    // Simulate API response
    this.chatService.sendQuestion(userQuestion).subscribe({
      next: (response: { answer: string }) => {
        // Update the last conversation with the received answer
        const lastMessageIndex = this.selectedChat.conversations.length - 1;
        this.selectedChat.conversations[lastMessageIndex].answer = response.answer;
    
        // Update the chat date
        this.selectedChat.date = new Date();
      },
      error: (error: any) => {
        // Handle errors gracefully
        console.error('API call failed:', error);
    
        const lastMessageIndex = this.selectedChat.conversations.length - 1;
        this.selectedChat.conversations[lastMessageIndex].answer =
          'Error fetching response. Please try again.';
    
        // Update the chat date
        this.selectedChat.date = new Date();
      },
      complete: () => {
        console.log('API call completed successfully.');
      },
    });
    
    this.userQuestion = ''; // Clear the input field
  }
  
  onKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault(); // Prevent new line in the textarea
      this.askQuestion(); // Trigger the askQuestion() method
    }
  }
  addConversation(question: string, answer: string) {
    this.chat.conversations.push({ question, answer });
  }

  adjustTextareaHeight(event: Event) {
    const textarea = event.target as HTMLTextAreaElement;
    textarea.style.height = 'auto'; // Reset height
    textarea.style.height = `${textarea.scrollHeight}px`; // Adjust to content
  }
}

