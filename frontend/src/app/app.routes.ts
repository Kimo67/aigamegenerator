import { Routes } from '@angular/router';
import { MainPageComponent } from './main-page/main-page.component';
import { BlockComponent } from './pages/blocks/block.component';

export const routes: Routes = [
    { path: '', component: MainPageComponent },
    { path: 'new-story', component: BlockComponent }
];
