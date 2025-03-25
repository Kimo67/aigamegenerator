export interface Block {
    id: number;
    parentId?: number;
    choices: { id: string; label: string }[];
    position?: { x: number; y: number };
    linkedChoiceId?: string;
  }
  