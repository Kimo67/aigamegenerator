import { Component } from '@angular/core';
import { BlockComponent } from './pages/blocks/block.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [BlockComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {}
