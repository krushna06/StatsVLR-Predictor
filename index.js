const fs = require('fs');
const path = require('path');
const axios = require('axios');
const readline = require('readline');

const BASE_TEAM_URL = "http://localhost:5000/api/v1/teams";
const BASE_PLAYER_URL = "http://localhost:5000/api/v1/players";
const REGIONS = ["na", "eu", "br", "ap", "kr", "ch", "jp", "lan", "las", "oce", "mn", "gc"];
const OUTPUT_DIR = path.join(__dirname, "dataset");
const TEAM_OUTPUT_FILE = path.join(OUTPUT_DIR, "allteams.json");
const PLAYER_OUTPUT_FILE = path.join(OUTPUT_DIR, "allplayers.json");
const LIMIT = 10;

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

async function fetchAllTeams() {
    let allTeams = [];
    let skippedRegions = [];
    
    for (const region of REGIONS) {
        let page = 1;
        while (true) {
            const url = `${BASE_TEAM_URL}?page=${page}&limit=${LIMIT}&region=${region}`;
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
    
    fs.writeFileSync(TEAM_OUTPUT_FILE, JSON.stringify(allTeams, null, 2));
    console.log(`Saved all teams data to ${TEAM_OUTPUT_FILE}`);
    
    if (skippedRegions.length > 0) {
        console.log(`Skipped regions due to errors: ${skippedRegions.join(", ")}`);
    }
}

async function fetchAllPlayers() {
    let allPlayers = [];
    let page = 1;
    
    while (true) {
        const url = `${BASE_PLAYER_URL}?page=${page}&limit=${LIMIT}`;
        try {
            const response = await axios.get(url);
            const data = response.data;
            
            if (!data || !data.data || data.data.length === 0) break;
            
            allPlayers.push(...data.data);
            console.log(`Fetched ${data.data.length} players from page ${page}`);
            
            if (!data.pagination.hasNextPage) break;
            
            page++;
        } catch (error) {
            console.error(`Error fetching players data, page ${page}:`, error.message);
            break;
        }
    }
    
    if (!fs.existsSync(OUTPUT_DIR)) {
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }
    
    fs.writeFileSync(PLAYER_OUTPUT_FILE, JSON.stringify(allPlayers, null, 2));
    console.log(`Saved all players data to ${PLAYER_OUTPUT_FILE}`);
}

function start() {
    rl.question("What operation do you want to perform? (1: Fetch Teams, 2: Fetch Players): ", (answer) => {
        if (answer === "1") {
            fetchAllTeams().then(() => rl.close());
        } else if (answer === "2") {
            fetchAllPlayers().then(() => rl.close());
        } else {
            console.log("Invalid option. Please enter 1 or 2.");
            rl.close();
        }
    });
}

start();
