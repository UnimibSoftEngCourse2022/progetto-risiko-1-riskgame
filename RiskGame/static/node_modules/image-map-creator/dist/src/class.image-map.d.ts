import { Area, AreaDefault } from "./class.area";
export declare class ImageMap {
    width: number;
    height: number;
    protected areas: Area[];
    protected name: string;
    hasDefaultArea: boolean;
    protected dArea: AreaDefault;
    protected lastId: number;
    /**
     * Contructor
     * @param {Area[]} areas
     * @param {string} name
     * @param {boolean} hasDefaultArea
     */
    constructor(width: number, height: number, areas?: Area[], name?: string, hasDefaultArea?: boolean);
    setFromObject(obj: Object): this;
    setName(name: string): this;
    getName(): string;
    setSize(width: number, height: number): this;
    setDefaultArea(bool: boolean): this;
    /**
     * Returns a copy of the area of the imageMap
     * @param {boolean} all with the default area (if exist) or not (default: true)
     * @returns {Area[]} a copy of the areas
     */
    getAreas(all?: boolean): Area[];
    isEmpty(): boolean;
    /**
     * Adds an Area at the end of the areas array, and returns the last inserted Area's id
     * @param {Area} area an area
     */
    addArea(area: Area, setId?: boolean): number;
    rmvArea(id: number): number;
    /**
     * Move an area up or down in the areas array
     * @param {number} id
     * @param {number} direction
     */
    moveArea(id: number, direction: number): number | false;
    shiftArea(): Area | undefined;
    popArea(): Area | undefined;
    insertArea(area: Area, index: number): number;
    areaIndex(id: number): number;
    isFirstArea(id: number): boolean;
    isLastArea(id: number): boolean;
    getNewId(): number;
    toHtml(scale?: number): string;
    toSvg(scale?: number): string;
    /** Removes every areas from the areas array */
    clearAreas(): this;
    setAreas(areas: Area[]): this;
}
