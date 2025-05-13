import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Block } from './core/models/block.model';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly baseUrl = 'http://localhost:8001/api';
  constructor(private http: HttpClient) {}

  getCases(): Observable<Block[]> {
    return this.http.get<Block[]>(this.baseUrl);
  }

  createCase(payload: Partial<Block>): Observable<Block> {
    return this.http.post<Block>(`${this.baseUrl}/case/`, payload);
  }

  getCase(id: number): Observable<Block> {
    return this.http.get<Block>(`${this.baseUrl}${id}/`);
  }

  updateCase(id: number, block: Partial<Block>): Observable<Block> {
    return this.http.put<Block>(`${this.baseUrl}${id}/`, block);
  }

  deleteCase(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}${id}/`);
  }
}
