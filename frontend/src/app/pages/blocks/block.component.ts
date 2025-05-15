import { Component, AfterViewInit, ElementRef, ViewChild, OnDestroy } from '@angular/core';
import { NgFor, NgIf } from "@angular/common";
import { FormsModule } from '@angular/forms';
import { Case, Reply } from '../../core/models/block.model';
import { ApiService } from '../../api.service';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-block',
  standalone: true,
  imports: [NgFor, NgIf, FormsModule],
  templateUrl: './block.component.html',
  styleUrls: ['./block.component.scss']
})
export class BlockComponent implements AfterViewInit, OnDestroy {

  personnages: string[] = [];

  private boundMouseMove = this.onMouseMove.bind(this);
  private boundMouseUp = this.onMouseUp.bind(this);

  currentOpenChoiceId: string | null = null;

  constructor(private apiService: ApiService) { }

  nextId = 2;

  blocks: Case[] = [
    {
      id: 1,
      command: '',
      parentId: null,
      choices: [],
      repliques: [],
      position: { x: 50, y: 50 }
    }
  ];


  lines: { line: any, linkedChoiceId: string }[] = [];
  occupiedPositions: Set<string> = new Set();

  @ViewChild('blockContainer', { static: false }) blockContainer!: ElementRef;

  ngAfterViewInit(): void {
    this.updateLines();
    setTimeout(() => this.addChoiceHoverListeners(), 150);
    window.addEventListener('mousemove', this.boundMouseMove);
    window.addEventListener('mouseup', this.boundMouseUp);

  }

  ngOnDestroy(): void {
      this.lines.forEach(item => item.line.remove());
      this.lines = [];    
      window.removeEventListener('mousemove', this.boundMouseMove);
      window.removeEventListener('mouseup', this.boundMouseUp); 
  }

  async handleCommandEnter(block: Case) {
    const prompt = block.command?.trim();
    if (!prompt) return;

    const payload: Partial<Case> = {
      prompt,
      parent: null,
      title: `Case ${this.nextId}`,
      story: 1,
      characters: ['MARIO', 'YOSHI']
    };

    try {
      const result = await firstValueFrom(this.apiService.createCase(payload)) as Case;
  
      const newChoice = {
        id: this.generateChoiceId(block.id, block.choices?.length || 0),
        label: 'Choix ' + ((block.choices?.length ?? 0) + 1)
      };

      const characters = await firstValueFrom(this.apiService.getCharacterList());

      this.personnages = characters.map((character) => character.name);
  
      result.repliques?.forEach((replique) => {
        this.addReply(block, replique)
      });
  
      if (!block.choices) block.choices = [];
      block.choices.push(newChoice);
  
      block.command = '';
    } catch (err) {
      console.error('Erreur lors de la création de la case', err);
    }
  }

  calculateNewPosition(parent: Case): { x: number; y: number } {
    const parentEl = document.getElementById(`block-${parent.id}`);
    const parentWidth = parentEl?.offsetWidth || 320;
    const parentHeight = parentEl?.offsetHeight || 300;

    const baseX = (parent.position?.x || 0) + parentWidth + 80;
    const parentY = parent.position?.y || 0;

    let yOffset = 0;
    let x = baseX;
    let y = parentY + yOffset;
    let positionKey = `${x},${y}`;
    const verticalSpacing = parentHeight + 60;

    while (this.occupiedPositions.has(positionKey)) {
      yOffset += verticalSpacing;
      y = parentY + yOffset;
      positionKey = `${x},${y}`;
    }

    this.occupiedPositions.add(positionKey);
    return { x, y };
  }


  addBlock(parentId: number) {
    const parent = this.blocks.find(b => b.id === parentId);
    if (!parent) return;

    const baseX = (parent.position?.x || 0) + 320;
    let baseY = parent.position?.y || 0;

    let yOffset = 0;
    let positionKey = `${baseX},${baseY + yOffset}`;
    while (this.occupiedPositions.has(positionKey)) {
      yOffset += 280;
      positionKey = `${baseX},${baseY + yOffset}`;
    }

    const x = baseX;
    const y = baseY + yOffset;

    this.blocks.push({
      id: this.nextId++,
      parentId,
      command: '',
      choices: [],
      repliques: [],
      position: { x, y }
    });

    this.occupiedPositions.add(positionKey);

    setTimeout(() => {
      this.updateLines();
      this.addChoiceHoverListeners();
    }, 50);
  }

  addBlockFromChoice(parentBlockId: number, choiceId: string) {
    const parent = this.blocks.find(b => b.id === parentBlockId);
    if (!parent) return;

    const alreadyLinked = this.blocks.some(
      b => b.parentId === parentBlockId && b.linkedChoiceId === choiceId
    );
    if (alreadyLinked) return;

    const parentElement = document.getElementById(`block-${parentBlockId}`);
    const parentWidth = parentElement?.offsetWidth || 320;
    const parentHeight = parentElement?.offsetHeight || 300;

    const baseX = (parent.position?.x || 0) + parentWidth + 80;
    const parentY = parent.position?.y || 0;

    let yOffset = 0;
    let x = baseX;
    let y = parentY + yOffset;
    let positionKey = `${x},${y}`;
    const verticalSpacing = parentHeight + 60;

    while (this.occupiedPositions.has(positionKey)) {
      yOffset += verticalSpacing;
      y = parentY + yOffset;
      positionKey = `${x},${y}`;
    }

    const newBlock: Case = {
      id: this.nextId++,
      parentId: parentBlockId,
      linkedChoiceId: choiceId,
      command: '',
      choices: [],
      repliques: [],
      position: { x, y }
    };

    this.blocks.push(newBlock);
    this.scrollToBlock(newBlock.id);
    this.occupiedPositions.add(positionKey);

    setTimeout(() => {
      this.updateLines();
      this.addChoiceHoverListeners();
    }, 50);
  }

  generateChoiceId(blockId: number, index: number): string {
    return `choice-${blockId}-${index}-${Math.floor(Math.random() * 100000)}`;
  }

  addChoice(block: Case) {
    const newChoice = {
      id: this.generateChoiceId(block.id, block.choices.length + 1),
      label: 'Choix ' + (block.choices.length + 1)
    };
    block.choices.push(newChoice);
  }

  removeChoice(blockId: number, choiceId: string) {
    const block = this.blocks.find(b => b.id === blockId);
    if (!block) return;

    block.choices = block.choices.filter(c => c.id !== choiceId);

    const childBlock = this.blocks.find(
      b => b.parentId === blockId && b.linkedChoiceId === choiceId
    );

    if (childBlock) {
      this.removeBlockRecursive(childBlock.id);
    }

    this.updateLines();
  }

  removeBlock(id: number) {
    this.blocks = this.blocks.filter(block => block.id !== id && block.parentId !== id);
    this.updateLines();
  }

  removeBlockRecursive(id: number) {
    const children = this.blocks.filter(b => b.parentId === id);
    children.forEach(child => this.removeBlockRecursive(child.id));

    const block = this.blocks.find(b => b.id === id);
    if (block?.position) {
      const key = `${block.position.x},${block.position.y}`;
      this.occupiedPositions.delete(key);
    }

    this.blocks = this.blocks.filter(b => b.id !== id);
  }

  updateLines() {
    this.lines.forEach(item => item.line.remove());
    this.lines = [];

    setTimeout(() => {
      const LeaderLine = (window as any).LeaderLine;
      if (!LeaderLine) return;

      this.blocks.forEach(block => {
        if (block.parentId && block.linkedChoiceId) {
          const parentChoiceElement = document.getElementById(block.linkedChoiceId);
          const childBlockElement = document.getElementById(`block-${block.id}`);

          if (parentChoiceElement && childBlockElement) {
            const line = new LeaderLine(parentChoiceElement, childBlockElement, {
              path: 'fluid',
              color: this.getColorForParent(block.parentId),
              size: 4,
              dash: { animation: true },
              startPlug: 'disc',
              endPlug: 'arrow2',
              startSocket: 'right',
              endSocket: 'left'
            });

            this.lines.push({ line, linkedChoiceId: block.linkedChoiceId });
          }
        }
      });
    }, 100);
  }

  addChoiceHoverListeners() {
    this.blocks.forEach(block => {
      block.choices.forEach(choice => {
        const el = document.getElementById(choice.id);
        if (el) {
          el.addEventListener('mouseenter', () => this.highlightLine(choice.id));
          el.addEventListener('mouseleave', () => this.resetLine(choice.id));
        }
      });
    });
  }

  highlightLine(choiceId: string) {
    const item = this.lines.find(l => l.linkedChoiceId === choiceId);
    if (item) {
      item.line.setOptions({
        size: 6,
        color: '#FFD700',
        outline: true,
        outlineColor: '#f1f1f1'
      });
    }
  }

  resetLine(choiceId: string) {
    const item = this.lines.find(l => l.linkedChoiceId === choiceId);
    if (item) {
      const parentBlock = this.blocks.find(b => b.linkedChoiceId === choiceId);
      item.line.setOptions({
        size: 4,
        color: this.getColorForParent(parentBlock?.parentId || 0),
        outline: false
      });
    }
  }

  private parentColors = new Map<number, string>();

  private getColorForParent(parentId: number): string {
    if (!this.parentColors.has(parentId)) {
      const colors = [
        '#0078FF', '#00C6FF', '#00D563', '#FF7E67',
        '#FF3CAC', '#6F42C1', '#FFD700', '#FF6F91', '#17C3B2'
      ];
      const index = this.parentColors.size % colors.length;
      this.parentColors.set(parentId, colors[index]);
    }
    return this.parentColors.get(parentId)!;
  }

  getBlockBorderColor(block: Case): string {
    return block.parentId ? this.getColorForParent(block.parentId) : 'black';
  }

  stopEditingChoice(choice: any) {
    choice.editing = false;
  }  

  toggleSettings(choice: any) {
    if (this.currentOpenChoiceId === choice.id) {
      this.currentOpenChoiceId = null;
    } else {
      this.currentOpenChoiceId = choice.id;
    }
  }

  startEditingChoice(choice: any) {
    choice.editing = true;
    choice.openSettings = false;
  }

  scrollToBlock(blockId: number) {
    setTimeout(() => {
      const element = document.getElementById(`block-${blockId}`);
      if (element) {
        const rect = element.getBoundingClientRect();
        const scrollTop = window.scrollY + rect.top - window.innerHeight / 2 + rect.height / 2;
        const scrollLeft = window.scrollX + rect.left - window.innerWidth / 2 + rect.width / 2;

        window.scrollTo({
          top: scrollTop,
          left: scrollLeft,
          behavior: 'smooth'
        });
      }
    }, 100);
  }

  generateReplyId(blockId: number, index: number): string {
    return `reply-${blockId}-${index}-${Math.floor(Math.random() * 100000)}`;
  }

  addNewReply(block: Case) {
    const newReply = {
      texte: '',
      emotion: 'NEUTRAL',
      personnage: 'Personnage 1'
    };

    block.repliques.push(newReply);
  }

  addReply(block: Case, reply: Reply) {
    block.repliques.push(reply);
  }

  removeReply(block: Case, replyToRemove: any) {
    block.repliques = block.repliques.filter(reply =>
      reply !== replyToRemove
    );
  }

  private isDragging = false;
  private dragOffset = { x: 0, y: 0 };
  private draggedBlock: Case | null = null;

  onMouseDown(event: MouseEvent, block: Case) {
    const target = event.target as HTMLElement;
    const interactiveTags = ['INPUT', 'TEXTAREA', 'SELECT', 'BUTTON'];
  
    if (interactiveTags.includes(target.tagName)) return;
  
    this.isDragging = true;
    this.draggedBlock = block;
  
    const element = target.closest('.block') as HTMLElement;
    const rect = element.getBoundingClientRect();
  
    this.dragOffset.x = event.clientX - rect.left;
    this.dragOffset.y = event.clientY - rect.top;
  
    event.preventDefault();
  }  

  onMouseMove(event: MouseEvent) {
    if (!this.isDragging || !this.draggedBlock) return;

    const containerRect = this.blockContainer.nativeElement.getBoundingClientRect();
    const x = event.clientX - containerRect.left - this.dragOffset.x;
    const y = event.clientY - containerRect.top - this.dragOffset.y;

    this.draggedBlock.position = { x, y };

    this.updateLines();
  }

  onMouseUp() {
    this.isDragging = false;
    this.draggedBlock = null;
  }

}
