import { Component, EventEmitter, HostListener, Output } from '@angular/core';
import { ChatServiceService } from '../chat-service.service';
import { Chat } from 'src/model/model';

@Component({
  selector: 'app-chat-sidebar',
  templateUrl: './chat-sidebar.component.html',
  styleUrls: ['./chat-sidebar.component.css'],
})
export class ChatSidebarComponent {
  selectedChatIndex: number | null = null;
  hoveredChatIndex: number | null = null;
  hoveredOptionIndex: number | null = null;
  chatList = this.chatService.getChats();
  selectedChat: Chat | null = null;
  @Output() chatSelected = new EventEmitter<number>();
  
  constructor(private chatService: ChatServiceService) {

  }
  ngOnInit() {
    this.chatList = this.chatService.getChats();
    this.chatService.selectedChat$.subscribe((chat) => {
      this.selectedChat = chat;
    });
  }

  // Create a new chat
  createNewChat() {
    const newChat: Chat = { title: 'Nouvelle conversation', conversations: [], date: new Date() };
    this.chatService.saveChats(newChat);
    this.chatList = this.chatService.getChats();
    this.selectedChatIndex = this.chatList.length - 1; // Set to the last chat index
    this.chatService.selectChat(this.selectedChatIndex);
    this.chatSelected.emit(this.selectedChatIndex);
  }
  

  // Select a chat
  selectChat(index: number) {
    this.selectedChatIndex = index;
    this.chatService.selectChat(this.selectedChatIndex)
    this.chatSelected.emit(index);
  }

  // Open options (placeholder for rename/delete logic)
  openOptions(index: number, event: MouseEvent) {
    event.stopPropagation();
    console.log(`Options for chat ${index}`);
    this.openedOptionsIndex = index;
  }


openedOptionsIndex: number | null = null;

displayOptions(index: number): void {
  this.hoveredOptionIndex = index;
}

hideOptions(): void {
  this.hoveredOptionIndex = null;
}
hideMenu():void{
  this.openedOptionsIndex = null;
}
changeColor(index: number): void {
  this.hoveredChatIndex = index
}

@HostListener('document:click', ['$event'])
onDocumentClick(event: MouseEvent) {
  this.hideMenu(); 
}
renameChat(index: number): void {
  // Logic to rename the chat
  console.log(`Rename chat at index ${index}`);
}

deleteChat(index: number) {
  // Remove the chat from the list
  this.chatList.splice(index, 1);

  // Handle selection of the next chat
  if (this.chatList.length > 0) {
    if (index > 0) {
      // Select the chat before the deleted one
      this.chatService.setSelectedChat(this.chatList[index - 1]);
    } else {
      // If the first chat was deleted, select the new first chat
      this.chatService.setSelectedChat(this.chatList[0]);
    }
  } else {
    // If no chats are left, clear the selection
    this.selectedChat = null;

  }
}


}
