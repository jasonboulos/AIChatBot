import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Chat } from 'src/model/model';
import { BehaviorSubject } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class ChatServiceService {

  private askUrl = 'http://127.0.0.1:8000/ask';
  private getUrl = 'http://127.0.0.1:8000/health';
  private summarizeUrl = 'http://127.0.0.1:8000/summarize';
  constructor(private http: HttpClient) { }
  private chats: Chat[] = [];

  getChats() {
    return this.chats;
  }
  private selectedChatSubject = new BehaviorSubject<Chat | null>(null); 
  selectedChat$ = this.selectedChatSubject.asObservable();
  saveChats(newChat : Chat) {
    this.chats.push(newChat);
    this.selectedChatSubject.next(newChat);
  }

  checkStatus():Observable<{status:string}>{
    return this.http.get<{status: string}>(this.getUrl);
  }
  sendQuestion(question: string): Observable<{ answer: string , sources: string[]}> {
    return this.http.post<{ answer: string , sources: string[]}>(this.askUrl, { question }); 
  }

  summarizeQuestion(question: string): Observable<{title: string}>{
    return this.http.post<{title: string}>(this.summarizeUrl, {question});
  }
  selectChat(index: number) {
    this.selectedChatSubject.next(this.chats[index]);
  }

  setSelectedChat(chat: Chat) {
    this.selectedChatSubject.next(chat);
  }
}
