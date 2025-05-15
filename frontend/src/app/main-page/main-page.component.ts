import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ApiService } from '../api.service';
import { firstValueFrom } from 'rxjs';
import { FormsModule } from '@angular/forms';
interface Particle {
  id: number;
  x: number;
  y: number;
  size: number;
}

interface Theme {
  bgClass: string;
  icon: string;
  particles: Particle[];
}

@Component({
  selector: 'app-main-page',
  standalone: true,
  imports: [RouterModule, CommonModule, FormsModule],
  templateUrl: './main-page.component.html',
  styleUrl: './main-page.component.scss'
})
export class MainPageComponent {
  activeTheme: string | null = null;
  storyName: string = '';
  EmptyStoryName: boolean = false;

  // Bootstrap Icons - utilisation de classes au lieu de SVG
  themes: Record<string, Theme> = {
    fantasy: {
      bgClass: 'bg-gradient-to-br from-purple-900 to-indigo-600',
      icon: 'bi bi-stars',
      particles: Array(34).fill(0).map((_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 2 + Math.random() * 3,
      }))
    },
    scifi: {
      bgClass: 'bg-gradient-to-br from-blue-900 to-cyan-700',
      icon: 'bi bi-lightning-charge-fill text-cyan-300',
      particles: Array(31).fill(0).map((_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 1 + Math.random() * 2,
      }))
    },
    adventure: {
      bgClass: 'bg-gradient-to-br from-green-800 to-yellow-600',
      icon: 'bi bi-compass text-green-200',
      particles: Array(25).fill(0).map((_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 2 + Math.random() * 4,
      }))
    },
    default: {
      bgClass: 'bg-gradient-to-br from-green-600 to-emerald-400',
      icon: 'bi bi-cloud-fill',
      particles: Array(30).fill(0).map((_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 2 + Math.random() * 3,
      }))
    }
  };

  // Icône par défaut du soleil
  defaultIcon = 'bi bi-sun-fill';
  constructor(private apiService: ApiService, private router: Router) { }
  
  get currentTheme(): Theme {
    return this.activeTheme ? this.themes[this.activeTheme] : this.themes['default'];
  }
  
  setActiveTheme(theme: string | null): void {
    this.activeTheme = theme;
  }
  
  // Cette méthode n'est plus utilisée car nous utilisons directement les classes Bootstrap
  getIconClass(themeKey: string | null): string {
    if (!themeKey) return this.defaultIcon;
    return this.themes[themeKey]?.icon || this.defaultIcon;
  }

   async goToNewStory(name: string) {
    if(!name) {
      this.EmptyStoryName = true; // Active la classe erreur
      return;
    }
    this.EmptyStoryName = false; // Réinitialise l'erreur si tout va bien
    const story = await firstValueFrom(this.apiService.createStory(name))
    this.router.navigate(['/new-story',  story.id]);
  }
}