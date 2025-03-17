const fs = require('fs');
const path = require('path');
const axios = require('axios');

const BASE_URL = "http://localhost:5000/api/v1/teams";
const REGIONS = ["na", "eu", "br", "ap", "kr", "ch", "jp", "lan", "las", "oce", "mn", "gc"];
const OUTPUT_DIR = path.join(__dirname, "dataset");
const OUTPUT_FILE = path.join(OUTPUT_DIR, "allteams.json");
const LIMIT = 10;

async function fetchAllTeams() {
    let allTeams = [];
    let skippedRegions = [];
    
    for (const region of REGIONS) {
        let page = 1;
        while (true) {
            const url = `${BASE_URL}?page=${page}&limit=${LIMIT}&region=${region}`;
            try {
                const response = await axios.get(url);
                const data = response.data;
                
                if (!data || !data.data || data.data.length === 0) break;
                
                allTeams.push(...data.data);
                console.log(`Fetched ${data.data.length} teams from region ${region}, page ${page}`);
                
                if (!data.pagination.hasNextPage) break;
                
                page++;
            } catch (error) {
                if (error.response && error.response.status === 400) {
                    console.warn(`Skipping region ${region} due to bad request (400)`);
                    skippedRegions.push(region);
                    break;
                }
                console.error(`Error fetching data for region ${region}, page ${page}:`, error.message);
                break;
            }
        }
    }
    
    if (!fs.existsSync(OUTPUT_DIR)) {
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }
    
    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(allTeams, null, 2));
    console.log(`Saved all teams data to ${OUTPUT_FILE}`);
    
    if (skippedRegions.length > 0) {
        console.log(`Skipped regions due to errors: ${skippedRegions.join(", ")}`);
    }
}

fetchAllTeams();