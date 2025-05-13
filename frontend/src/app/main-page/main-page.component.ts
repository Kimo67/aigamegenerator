import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
interface Particle {
  id: number;
  x: number;
  y: number;
  size: number;
  speed: number;
}

interface Theme {
  bgClass: string;
  icon: string;
  particles: Particle[];
}

@Component({
  selector: 'app-main-page',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './main-page.component.html',
  styleUrl: './main-page.component.scss'
})
export class MainPageComponent {
  activeTheme: string | null = null;
  
  // Bootstrap Icons - utilisation de classes au lieu de SVG
  themes: Record<string, Theme> = {
    fantasy: {
      bgClass: 'bg-gradient-to-br from-purple-900 to-indigo-600',
      icon: 'bi bi-stars',
      particles: Array(10).fill(0).map((_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 2 + Math.random() * 3,
        speed: 0.2 + Math.random() * 0.3,
      }))
    },
    scifi: {
      bgClass: 'bg-gradient-to-br from-blue-900 to-cyan-700',
      icon: 'bi bi-lightning-charge-fill text-cyan-300',
      particles: Array(15).fill(0).map((_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 1 + Math.random() * 2,
        speed: 0.3 + Math.random() * 0.4,
      }))
    },
    adventure: {
      bgClass: 'bg-gradient-to-br from-green-800 to-yellow-600',
      icon: 'bi bi-compass text-green-200',
      particles: Array(8).fill(0).map((_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 2 + Math.random() * 4,
        speed: 0.1 + Math.random() * 0.2,
      }))
    },
    default: {
      bgClass: 'bg-gradient-to-br from-green-600 to-emerald-400',
      icon: 'bi bi-cloud-fill',
      particles: Array(10).fill(0).map((_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 2 + Math.random() * 3,
        speed: 0.15 + Math.random() * 0.2,
      }))
    }
  };

  // Icône par défaut du soleil
  defaultIcon = 'bi bi-sun-fill';
  
  constructor(private sanitizer: DomSanitizer) {}
  
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
}