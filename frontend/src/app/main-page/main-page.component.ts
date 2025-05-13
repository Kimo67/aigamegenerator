//main-page.component.ts
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
  iconColor?: string; // Couleur de l'icône
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
  
  // Icônes SVG en tant que strings - couleurs ajustées
  sparklesIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-yellow-300"><path d="M12 3v18"></path><path d="m9 6 3-3 3 3"></path><path d="m9 18 3 3 3-3"></path><path d="M3 12h18"></path><path d="m6 9-3 3 3 3"></path><path d="m18 9 3 3-3 3"></path></svg>';
  
  zapIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-cyan-300"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>';
  
  mountainIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-green-200"><path d="m8 3 4 8 5-5 5 15H2L8 3z"></path></svg>';
  
  cloudIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-white"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"></path></svg>';
  
  sunIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-yellow-300"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2"></path><path d="M12 20v2"></path><path d="m4.93 4.93 1.41 1.41"></path><path d="m17.66 17.66 1.41 1.41"></path><path d="M2 12h2"></path><path d="M20 12h2"></path><path d="m6.34 17.66-1.41 1.41"></path><path d="m19.07 4.93-1.41 1.41"></path></svg>';
  
  // Optimisation du nombre de particules pour améliorer les performances
  themes: Record<string, Theme> = {
    fantasy: {
      bgClass: 'bg-gradient-to-br from-purple-900 to-indigo-600',
      icon: this.sparklesIcon,
      iconColor: 'white',
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
      icon: this.zapIcon,
      iconColor: 'cyan-300',
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
      icon: this.mountainIcon,
      iconColor: 'green-200',
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
      icon: this.cloudIcon,
      particles: Array(10).fill(0).map((_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 2 + Math.random() * 3,
        speed: 0.15 + Math.random() * 0.2,
      }))
    }
  };
  
  constructor(private sanitizer: DomSanitizer) {}
  
  get currentTheme(): Theme {
    return this.activeTheme ? this.themes[this.activeTheme] : this.themes['default'];
  }
  
  setActiveTheme(theme: string | null): void {
    this.activeTheme = theme;
  }
  
  getSafeIcon(icon: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(icon);
  }
  
}