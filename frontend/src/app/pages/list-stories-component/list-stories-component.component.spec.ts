import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListStoriesComponentComponent } from './list-stories-component.component';

describe('ListStoriesComponentComponent', () => {
  let component: ListStoriesComponentComponent;
  let fixture: ComponentFixture<ListStoriesComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListStoriesComponentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListStoriesComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
