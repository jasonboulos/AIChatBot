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
  @Output() chatSelected = new EventEmitter<number>();
  
  constructor(private chatService: ChatServiceService) {

  }

  // Create a new chat
  createNewChat() {
    const newChat : Chat = { title: 'NewChat',conversations :[], date: new Date() };
    this.chatService.saveChats(newChat);

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

deleteChat(index: number): void {
  // Logic to delete the chat
  console.log(`Delete chat at index ${index}`);
}

}
