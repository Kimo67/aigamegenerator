import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Case, Character, Story } from './core/models/block.model';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly baseUrl = 'http://localhost:8001/api';
  constructor(private http: HttpClient) { }

  createCase(payload: Partial<Case>): Observable<Case> {
    return this.http.post<Case>(`${this.baseUrl}/case/`, payload);
  }

  getCharacterList(): Observable<Character[]> {
    return this.http.get<Character[]>(`${this.baseUrl}/characters`);
  }

  getStories(): Observable<Story[]> {
    return this.http.get<Story[]>(`${this.baseUrl}/stories`)
  }

  getCasesByStoryId(storyId: number): Observable<Case[]> {
    const params = new HttpParams().set('story', storyId.toString());
    return this.http.get<Case[]>(`${this.baseUrl}/case`, { params })
  }
}
