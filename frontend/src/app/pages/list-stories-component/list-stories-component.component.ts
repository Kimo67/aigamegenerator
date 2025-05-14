import { Component } from '@angular/core';
import { Story } from '../../core/models/block.model';
import { ApiService } from '../../api.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-list-stories-component',
  imports: [CommonModule],
  templateUrl: './list-stories-component.component.html',
  styleUrl: './list-stories-component.component.scss'
})
export class ListStoriesComponentComponent {

  stories: Story[] = [];

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

}
