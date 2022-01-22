import { imageMapCreator } from "./p5.image-map-creator";
/**
 * Class representing the semi transparent layer which can appear on top of the background
 * @param {number} speed the speed of the opacity animation (1-255, default 15)
 */
export declare class BgLayer {
    protected iMap: imageMapCreator;
    protected speed: number;
    protected alpha: number;
    protected over: boolean;
    constructor(iMap: imageMapCreator, speed?: number, alpha?: number, over?: boolean);
    appear(): void;
    disappear(): void;
    display(): void;
}
