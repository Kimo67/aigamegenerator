import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'https://localhost:8080'; 

  constructor(private http: HttpClient) {}

  getData(): Observable<any> {
    return this.http.get(`${this.baseUrl}/data`);
  }

  postData(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/data`, data);
  }

  updateData(id: number, data: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/data/${id}`, data);
  }

  deleteData(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/data/${id}`);
  }
}
