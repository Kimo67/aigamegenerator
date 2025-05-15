import { Routes } from '@angular/router';
import { MainPageComponent } from './main-page/main-page.component';
import { BlockComponent } from './pages/blocks/block.component';
import { ListStoriesComponentComponent } from './pages/list-stories-component/list-stories-component.component';

export const routes: Routes = [
    { path: '', component: MainPageComponent },
    { path: 'new-story/:id', component: BlockComponent },
    { path: 'load-story', component: ListStoriesComponentComponent }
];
