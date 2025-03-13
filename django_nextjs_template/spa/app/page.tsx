import { Metadata } from 'next';
import { Grid2 as Grid } from '@mui/material';


export async function generateMetadata(): Promise<Metadata> {
    return {};
}


export default async function Page() {
    return (
        <Grid container size={{xs:12, sm:8, md:8, lg:9}} spacing={2}>
            <Grid size={{xs:12}} spacing={2} container>
                Template Project main page
            </Grid>
        </Grid>
    )
}