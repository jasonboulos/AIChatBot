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
        title:"Nouvelle Conversation",
        conversations: [],
        date: new Date()
      }
      this.checkStatus();
    }
    
    
  }
  status: string | undefined;
  userQuestion: string = ''; // User input for question

  askQuestion() {
    if (!this.userQuestion.trim()) {
      return; // Avoid empty questions
    }
    
    const userQuestion = this.userQuestion; // Store the user's question
    // Push a new conversation into the chat's conversations list
    const newConversation = { question:userQuestion, answer: 'Typing...', sources: [] };
    this.selectedChat.conversations.push(newConversation);
    
    if (!this.chatService.getChats().includes(this.selectedChat) || this.selectedChat.title ==='Nouvelle conversation') {
      this.chatService.summarizeQuestion(userQuestion).subscribe({
        next: (response: { title: string }) => {
          const title = response.title;
          this.selectedChat.title = title;
          if(!this.chatService.getChats().includes(this.selectedChat)){
            this.chatService.saveChats(this.selectedChat)
            
          } 
          this.chatService.setSelectedChat(this.selectedChat);
        },
        error: (error: any) => {
          console.error('API call failed:', error);
        }
      });
    }
    
    this.chatService.sendQuestion(userQuestion).subscribe({
      next: (response: { answer: string, sources: string[]}) => {
        // Update the last conversation with the received answer
        const lastMessageIndex = this.selectedChat.conversations.length - 1;
        this.selectedChat.conversations[lastMessageIndex].answer = response.answer;
        this.selectedChat.conversations[lastMessageIndex].sources = response.sources;
    
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
    this.selectedChat.conversations.push({ question, answer });
  }
  formatSourceName(source: string): string {
    // Clean up file names
    return source
      .replace(/\.pdf$/, '')
      .replace(/_/g, ' ')
      .replace(/\b\w/g, c => c.toUpperCase());
  }
  toggleSources(convo: Chat) {
    convo.showSources = !convo.showSources;
  }
  adjustTextareaHeight(event: Event) {
    const textarea = event.target as HTMLTextAreaElement;
    textarea.style.height = 'auto'; // Reset height
    textarea.style.height = `${textarea.scrollHeight}px`; // Adjust to content
  }
  checkStatus() {
    this.chatService.checkStatus().subscribe(
      (response) => {
        this.status = response.status;
        console.log('Status:', this.status);
      },
      (error) => {
        console.error('Error:', error);
      }
    );
  }
}
