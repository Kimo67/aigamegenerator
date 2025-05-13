import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { routes } from './app.routes'; // tu peux créer ce fichier

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterModule], // ← Import essentiel pour <router-outlet>
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {}

