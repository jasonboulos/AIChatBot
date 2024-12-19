import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Chat } from 'src/model/model';
import { BehaviorSubject } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class ChatServiceService {

  private apiUrl = 'http://127.0.0.1:8000/ask';
  
  constructor(private http: HttpClient) { }
  private chats: Chat[] = [];

  getChats() {
    return this.chats;
  }
  private selectedChatSubject = new BehaviorSubject(this.chats[0]); // Default to first chat
  selectedChat$ = this.selectedChatSubject.asObservable();
  saveChats(newChat : Chat) {
    this.chats.push(newChat);
    this.selectedChatSubject.next(newChat)

  }
  sendQuestion(question: string): Observable<{ answer: string }> {
    return this.http.post<{ answer: string }>(this.apiUrl, { question }); 
  }
  selectChat(index: number) {
    this.selectedChatSubject.next(this.chats[index]);
  }
}
