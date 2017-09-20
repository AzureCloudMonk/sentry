import React from 'react';
import _ from 'lodash';

import EventDataSection from './eventDataSection';
import EventErrorItem from './errorItem';
import SentryTypes from '../../proptypes';
import {t, tn} from '../../locale';

const EventErrors = React.createClass({
  propTypes: {
    group: SentryTypes.Group.isRequired,
    event: SentryTypes.Event.isRequired
  },

  getInitialState() {
    return {
      isOpen: false
    };
  },

  shouldComponentUpdate(nextProps, nextState) {
    if (this.state.isOpen != nextState.isOpen) {
      return true;
    }
    return this.props.event.id !== nextProps.event.id;
  },

  toggle() {
    this.setState({isOpen: !this.state.isOpen});
  },

  uniqueErrors(errors) {
    return _.uniqBy(errors, _.isEqual);
  },

  render() {
    let errors = this.uniqueErrors(this.props.event.errors);
    let numErrors = errors.length;
    let isOpen = this.state.isOpen;
    return (
      <EventDataSection
        group={this.props.group}
        event={this.props.event}
        type="errors"
        className="errors">
        <span className="icon icon-alert" />
        <p>
          <a className="pull-right" onClick={this.toggle}>
            {isOpen ? t('Hide') : t('Show')}
          </a>
          {tn(
            'There was %d error encountered while processing this event',
            'There were %d errors encountered while processing this event',
            numErrors
          )}
        </p>
        <ul style={{display: isOpen ? 'block' : 'none'}}>
          {errors.map((error, errorIdx) => {
            return <EventErrorItem key={errorIdx} error={error} />;
          })}
        </ul>
      </EventDataSection>
    );
  }
});

export default EventErrors;
