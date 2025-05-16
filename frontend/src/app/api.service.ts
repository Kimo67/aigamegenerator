import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Case, Character, RenpyResponse, Story } from './core/models/block.model';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly baseUrl = 'http://localhost:8001';
  constructor(private http: HttpClient) { }

  createCase(payload: Partial<Case>): Observable<Case> {
    return this.http.post<Case>(`${this.baseUrl}/api/case/`, payload);
  }

  getCharacterList(): Observable<Character[]> {
    return this.http.get<Character[]>(`${this.baseUrl}/api/characters`);
  }

  getStories(): Observable<Story[]> {
    return this.http.get<Story[]>(`${this.baseUrl}/api/stories`)
  }

  getCasesByStoryId(storyId: number): Observable<Case[]> {
    const params = new HttpParams().set('story', storyId.toString());
    return this.http.get<Case[]>(`${this.baseUrl}/api/case`, { params })
  }

  createStory(name: string) : Observable<Story> {
    return this.http.post<Story>(`${this.baseUrl}/api/stories/`, {
      name
    })
  }

  exporterRenpy() : Observable<RenpyResponse> {
    return this.http.get<RenpyResponse>(`${this.baseUrl}/api/stories/renpy`);
  }
}
