import { Component } from '@angular/core';
import { Case, Character, Story } from '../../core/models/block.model';
import { ApiService } from '../../api.service';
import { CommonModule } from '@angular/common';
import { BlockComponent } from '../blocks/block.component';
import { firstValueFrom } from 'rxjs';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-list-stories-component',
  imports: [CommonModule, BlockComponent, RouterModule],
  templateUrl: './list-stories-component.component.html',
  styleUrl: './list-stories-component.component.scss'
})
export class ListStoriesComponentComponent {
particles = Array.from({ length: 30 }, (_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 2 + Math.random() * 3,
      }));
      
  stories: Story[] = [];
  selectedStoryId: number | null = null;
  storyBlocks: Case[] = [];
  personnages: string[] = [];

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {

    this.apiService.getStories().subscribe({
      next: (data) => {
        this.stories = data;
      },
      error: (err) => {
        console.error('Erreur lors du chargement des stories', err);
      }
    });
  }

  async selectStory(storyId: number) {
    this.selectedStoryId = storyId;

    try {
      const blocks = await firstValueFrom(this.apiService.getCasesByStoryId(storyId));
      const personnages = await firstValueFrom(this.apiService.getCharacterList())
      this.storyBlocks = blocks.filter((bloc) => bloc.story === storyId);
      this.personnages = personnages.map((character) => character.name);
    } catch (err) {
      console.error('Erreur lors de la récupération des blocs', err);
    }
  }

}
