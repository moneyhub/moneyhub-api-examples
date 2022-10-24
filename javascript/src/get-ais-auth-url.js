import config from './config.js';
import { Moneyhub } from '@mft/moneyhub-api-client';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const args = yargs(hideBin(process.argv)).option('state', {
  alias: 's',
  describe: 'state from original authorisation URL',
  default: 'foo',
}).argv;

const main = async () => {
  const moneyhub = await Moneyhub(config);
  const user = await moneyhub.registerUser({});
  const url = await moneyhub.getAuthorizeUrlForCreatedUser({
    state: args.state,
    userId: user.userId,
    bankId: 'test',
  });
  console.log(url);
};

main();
