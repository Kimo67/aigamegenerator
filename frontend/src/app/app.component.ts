import { Component } from '@angular/core';
import { ChatComponent } from './pages/chat/chat.component';
import { BlockComponent } from './pages/blocks/block.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ChatComponent, BlockComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {}
