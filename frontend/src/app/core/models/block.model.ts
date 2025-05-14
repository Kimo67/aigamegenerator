/*export interface Choice {
  id: string;
  label: string;
  editing?: boolean;
}

export interface Reply {
  id: string;
  character: string;
  text: string;
  tone: string;
}

export interface Block {
  id: number;
  parentId?: number;
  linkedChoiceId?: string;
  choices: Choice[];
  replies?: Reply[];
  position?: { x: number; y: number };
  command?: string;
}*/

export interface Reply {
  texte: string;
  emotion: string;
  personnage: string;
}

export interface Choice {
  id: string;
  label: string;
  editing?: boolean;
}

export interface Case {
  id: number;
  title?: string;
  prompt?: string;
  command?: string;
  story?: number;
  parentId?: number | null;
  parent?: number | null;
  linkedChoiceId?: string;
  choices: Choice[];
  repliques: Reply[];
  position?: { x: number; y: number };
  characters?: string[];
}

export interface Character {
  name: string,
}

export interface Story {
  id: string,
  name: string
}