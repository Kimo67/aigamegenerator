import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-chat',
  standalone: true,
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss'],
  imports: [CommonModule, FormsModule]
})
export class ChatComponent {
  isChatOpen = false;
  messages = [
    { text: 'Bonjour ! Comment puis-je vous aider ?', sender: 'bot' }
  ];
  newMessage = '';

  toggleChat() {
    this.isChatOpen = !this.isChatOpen;
  }

  sendMessage() {
    const userMessage = this.newMessage.trim();
    if (userMessage) {
      this.messages.push({ text: userMessage, sender: 'me' });
  
      setTimeout(() => {
        this.messages.push({
          text: this.generateBotResponse(userMessage),
          sender: 'bot'
        });
      }, 1000);
  
      this.newMessage = '';
    }
  }
  

  generateBotResponse(userMessage: string): string {
    const msg = userMessage.toLowerCase();
  
    if (msg.includes('bonjour')) {
      return "Bonjour ! Comment puis-je vous aider ?";
    } else if (msg.includes('hamid')) {
      return "Ravi de te voir Hamid";
    } else if (msg.includes('merci')) {
      return "Avec plaisir !";
    } else {
      return "Désolé, je ne comprends pas encore cette question.";
    }
  }
  
}
