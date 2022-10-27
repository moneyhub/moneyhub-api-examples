import config from './config.js';
import { Moneyhub } from '@mft/moneyhub-api-client';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const args = yargs(hideBin(process.argv)).option('state', {
  alias: 's',
  describe: 'state for original authorisation URL',
  default: 'foo',
}).option('nonce', {
  alias: 'n',
  describe: 'nonce for original authorisation URL',
  default: 'bar',
}).argv;

const main = async () => {
  const moneyhub = await Moneyhub(config);
  const user = await moneyhub.registerUser({});
  const url = await moneyhub.getAuthorizeUrlForCreatedUser({
    state: args.state,
    nonce: args.nonce,
    userId: user.userId,
    bankId: 'test',
  });
  console.log(url);
};

main();
