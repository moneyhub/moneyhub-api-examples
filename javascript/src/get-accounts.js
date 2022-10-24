import config from './config.js';
import { Moneyhub } from '@mft/moneyhub-api-client';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const args = yargs(hideBin(process.argv)).option('userId', {
  alias: 'u',
  describe: 'userId to get accounts for',
}).argv;

const main = async () => {
  const moneyhub = await Moneyhub(config);
  const url = await moneyhub.getAccounts({
    userId: args.userId,
  });
  console.log(url);
};

main();
