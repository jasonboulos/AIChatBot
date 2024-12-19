import { Component, EventEmitter, Output } from '@angular/core';
import { ChatServiceService } from '../chat-service.service';
import { Chat } from 'src/model/model';

@Component({
  selector: 'app-chat-sidebar',
  templateUrl: './chat-sidebar.component.html',
  styleUrls: ['./chat-sidebar.component.css'],
})
export class ChatSidebarComponent {
  selectedChatIndex: number | null = null;
  chatList = this.chatService.getChats();
  @Output() chatSelected = new EventEmitter<number>();

  constructor(private chatService: ChatServiceService) {

  }

  // Create a new chat
  createNewChat() {
    const newChat : Chat = { title: 'New Chat',conversations :[], date: new Date() };
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
  }
}
