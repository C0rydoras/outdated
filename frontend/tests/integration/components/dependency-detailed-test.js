import { module, test } from 'qunit';
import { setupRenderingTest } from 'outdated/tests/helpers';
import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import { setupMirage } from 'ember-cli-mirage/test-support';
module('Integration | Component | dependency-detailed', function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  test('dependency-detailed renders correctly', async function (assert) {
    this.version = await this.server.create('version');

    await render(hbs`<DependencyDetailed @version={{this.version}} />`);
    assert
      .dom('[data-test-version-status]')
      .hasClass(`text-${this.version.status}`);
    assert
      .dom('[data-test-version-dependency-name]')
      .hasText(this.version.dependency.name);
    assert.dom('[data-test-version-version]').hasText(this.version.version);
    assert.dom('[data-test-version-eol-date]').exists();
    assert.dom('[data-test-version-release-date]').exists();
  });
});
